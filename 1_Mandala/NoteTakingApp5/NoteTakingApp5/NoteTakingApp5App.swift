import SwiftUI
import UIKit


import SwiftUI

@main
struct NoteTakingApp5App: App {
    @StateObject private var conversations = Conversations()

    var body: some Scene {
        WindowGroup {
            NavigationView {
                SidebarView(conversations: $conversations.items, selection: .constant(0))
                    .environmentObject(conversations)
                ContentView(conversation: $conversations.items[0])
                    .environmentObject(conversations)
                    
            }
            .accentColor(.purple)
        }
    }
}


class Conversations: ObservableObject {
    @Published var items: [Conversation] = [Conversation(messages: [Message(content: "Hello, how can I help you?", isUser: false)], title: "Untitled")]
}


struct TextView: UIViewRepresentable {
    @Binding var text: String
    
    func makeUIView(context: Context) -> UITextView {
        let textView = UITextView()
        textView.delegate = context.coordinator // Set delegate to the coordinator
        textView.isScrollEnabled = true
        textView.isUserInteractionEnabled = true
        textView.backgroundColor = UIColor.systemGray6
        textView.font = UIFont.systemFont(ofSize: 18)
        textView.textContainerInset = UIEdgeInsets(top: 18, left: 10, bottom: 18, right: 10)
        return textView
    }
    
    func updateUIView(_ uiView: UITextView, context: Context) {
        uiView.text = text
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator : NSObject, UITextViewDelegate {
        var parent: TextView

        init(_ parent: TextView) {
            self.parent = parent
        }

        func textViewDidChange(_ textView: UITextView) {
            self.parent.text = textView.text // Update the text binding when text view changes
        }
    }
}
