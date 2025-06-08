import SwiftUI

struct SidebarView: View {
    @Binding var conversations: [Conversation]
    @Binding var selection: Int?
    @State var showInputForm = false

    var body: some View {
        List(selection: $selection) {
            Image("i1")
                .resizable()
                .aspectRatio(contentMode: .fill)
                .frame(height: 150)
                .clipped()

            ForEach(conversations.indices, id: \.self) { index in
                NavigationLink(destination: ContentView(conversation: $conversations[index])) {
                    HStack {
                        Image(systemName: "text.bubble")
                        Spacer().frame(width: 10)
                        Text(conversations[index].title)
                        Spacer()
                        Image(systemName: "ellipsis")
                        Spacer().frame(width: 10)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.vertical, 2)
                    .background(selection == index ? Color.clear : Color.clear)
                    .accentColor(selection == index ? .white : .purple)
                }
                .buttonStyle(PlainButtonStyle())
                .tag(index)
            }
        }
                .listStyle(SidebarListStyle())
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .principal) {
                        Text("Mandala")
                        .fontWeight(.bold)
                    }
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button(action: {
                            showInputForm = true // show the input form when the button is pressed
                        }) {
                            Image(systemName: "plus")
                        }
                        .accentColor(.purple)
                    }
                }
                .background(Color.gray)
                .accentColor(.purple)
                .sheet(isPresented: $showInputForm) { // present the form as a sheet
                    InputFormView()
                }
            }
        }
