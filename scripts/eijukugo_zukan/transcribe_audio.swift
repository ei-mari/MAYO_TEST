import Foundation
import Speech

if CommandLine.arguments.count < 2 {
    fputs("usage: swift transcribe_audio.swift <audio-file>\n", stderr)
    exit(1)
}

let audioPath = CommandLine.arguments[1]
let audioURL = URL(fileURLWithPath: audioPath)
let semaphore = DispatchSemaphore(value: 0)

func printErrorAndExit(_ message: String) -> Never {
    fputs(message + "\n", stderr)
    exit(1)
}

SFSpeechRecognizer.requestAuthorization { status in
    guard status == .authorized else {
        printErrorAndExit("speech authorization failed: \(status.rawValue)")
    }

    guard let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US")) else {
        printErrorAndExit("failed to create recognizer")
    }

    let request = SFSpeechURLRecognitionRequest(url: audioURL)
    request.shouldReportPartialResults = false
    request.requiresOnDeviceRecognition = false

    recognizer.recognitionTask(with: request) { result, error in
        if let error {
            printErrorAndExit("recognition error: \(error.localizedDescription)")
        }

        guard let result else {
            return
        }

        if result.isFinal {
            print(result.bestTranscription.formattedString)
            for segment in result.bestTranscription.segments {
                let ts = String(format: "%.3f", segment.timestamp)
                let dur = String(format: "%.3f", segment.duration)
                print("\(ts)\t\(dur)\t\(segment.substring)")
            }
            semaphore.signal()
        }
    }
}

_ = semaphore.wait(timeout: .now() + 300)
