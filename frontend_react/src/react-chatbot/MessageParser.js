import axios from 'axios';

class MessageParser {
  constructor(actionProvider, state, createChatBotMessage) {
    this.actionProvider = actionProvider;
    this.state = state;
    this.createChatBotMessage = createChatBotMessage;
  }

  async parse(incomingMessage) {
    try {
      const response = await axios.post('http://localhost:8000/process_message', {
        incoming_message: incomingMessage,
        chat_history: this.state.messages.map(msg => msg.message),
      });

      const reply = response.data.reply;
      this.actionProvider.sendBotResponse(reply);
    } catch (error) {
      console.error('Error processing message:', error);
      this.actionProvider.sendBotResponse("Sorry, I couldn't process that.");
    }
  }
}

export default MessageParser;
