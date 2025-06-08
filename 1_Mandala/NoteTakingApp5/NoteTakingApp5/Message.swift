import SwiftUI

struct Message: Identifiable, Hashable {
    var id = UUID()
    var content: String
    var isUser: Bool
}

struct Conversation: Identifiable {
    var id = UUID()
    var messages: [Message]
    var title: String
}
