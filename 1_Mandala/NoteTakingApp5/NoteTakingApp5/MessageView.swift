import SwiftUI

struct MessageView: View {
    var message: Message

    var body: some View {
        HStack {
            Text(message.content)
                .padding(.horizontal, 30)
                .padding(.vertical, 10)
                .foregroundColor(message.isUser ? .white : .black)
            Spacer()
        }
        .background(message.isUser ? Color.purple : Color.white)
        .frame(maxWidth: .infinity)
    }
}
