import SwiftUI

struct InputFormView: View {
    @EnvironmentObject var conversations: Conversations
    @Environment(\.presentationMode) var presentationMode
    @State private var userInput = ""
    @State private var newConversation = Conversation(messages: [], title: "")
    @State private var navigateToNewPage = false
    
    var body: some View {
        NavigationView {
            TabView {
                // First page
                VStack {
                                Text("What is Mandala?")
                                    .font(.largeTitle)
                                    .fontWeight(.bold)
                                    .foregroundColor(.purple)
                                    .offset(y: +20)
                                Image("c1")
                                    .resizable()
                                    .scaledToFit()
                                    .offset(y: -20)
                                    .clipped()
                                Text("A scalable psychological intervention.")
                                    .offset(y: -50)
                                    .foregroundColor(.gray)
                                Text("A chance to use Large Language Models to aid in clarifying your own thought.")
                                .offset(y: -50)
                                .foregroundColor(.gray)
                }
                .tag(0)
                
                // Second page
                VStack {
                    Text("Explore Your Past.")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.purple)
                        .offset(y: +10)
                    Text("Decide Your Future.")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.purple)
                        .offset(y: +10)
                    Image("c2")
                        .resizable()
                        .scaledToFit()
                        .offset(y: -50)
                        .clipped()
                    Text("AI will categorize your writing based on its purpose and subject")
                        .offset(y: -50)
                        .foregroundColor(.gray)
                    Text("and change its approach to helping you write as a result.")
                    .offset(y: -50)
                    .foregroundColor(.gray)
                }
                .tag(1)
                
                // Third page
                VStack {
                    Image("c3")
                        .resizable()
                        .scaledToFit()
                        .clipped()
                    Text("Let's get started! What would you like to talk about?")
                        .offset(y: -30)
                        .foregroundColor(.purple)
                    TextField("Your Thoughts", text: $userInput)
                        .padding()
                        .offset(y: -30)
                    Button("Submit") {
                        askGPT3(input: userInput) { assistantOutput in
                            newConversation = Conversation(messages: [], title: assistantOutput)
                            DispatchQueue.main.async {
                                conversations.items.append(newConversation)
                                navigateToNewPage = true // set to true to navigate
                                presentationMode.wrappedValue.dismiss() // dismiss the current view
                            }
                        }
                    }
                    .foregroundColor(.white)
                    .padding(.horizontal, 50)
                    .padding(.vertical, 5)
                    .background(Color.purple)
                    .cornerRadius(10)
                    .padding()
                    NavigationLink(destination: ContentView(conversation: $newConversation), isActive: $navigateToNewPage) {
                        EmptyView() // no visual representation
                    }
                }
                .tag(2)
            }
            .tabViewStyle(PageTabViewStyle())
            .indexViewStyle(PageIndexViewStyle(backgroundDisplayMode: .always))
        }
    }
    
    func askGPT3(input: String, completion: @escaping (String) -> Void) {
        let url = URL(string: "http://localhost:5001/api/askForTitle")! // match the route you defined in your flask app
        // replace with your server's URL
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let data = [
            "text2": input
        ]
        request.httpBody = try? JSONSerialization.data(withJSONObject: data)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                let json = try? JSONSerialization.jsonObject(with: data, options: [])
                if let dictionary = json as? [String: Any],
                   let assistant = dictionary["assistant"] as? String {
                    completion(assistant)
                }
            }
        }.resume()
    }
}
