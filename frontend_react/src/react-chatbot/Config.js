  // Config starter code
  import { createChatBotMessage } from "react-chatbot-kit";
  import CustomInput from './CustomInput';

  const config = {
    // change this to the message you want to be sent to the user when they first open the chatbot
    initialMessages: [createChatBotMessage(`Hey there!`)],
    customStyles: {
      botMessageBox: {
        backgroundColor: '#376B7E',
      },
      chatButton: {
        backgroundColor: '#5ccc9d',
      },
    },

    customComponents: {
      userInput: (props) => <CustomInput {...props} />, // Custom input component
    },

  }
  
  export default config