// CustomInput.js
import { useState } from 'react';

const CustomInput = ({ onSubmit }) => {
  const [message, setMessage] = useState("");

  return (
    <div className="flex items-center p-2 bg-red-200 rounded-lg">
      <input
        className="flex-grow p-2 rounded-l-lg border border-gray-300"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
      />
      <button
        className="bg-blue-500 text-white p-2 rounded-r-lg hover:bg-blue-600"
        onClick={() => {
          onSubmit(message);
          setMessage("");
        }}
      >
        Send
      </button>
    </div>
  );
};

export default CustomInput;
