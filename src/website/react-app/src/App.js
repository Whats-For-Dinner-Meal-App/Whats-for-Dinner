import React, { useState } from "react";
import "./App.css";
import TitleBar from "./components/TitleBar";
import Sidebar from "./components/Sidebar";
import RecipeBox from "./components/RecipeBox";
import ChefSVG from "./components/ChefSVG";
import Messages from "./components/Messages";
import Pantry from "./components/Pantry";

function App() {
  const [message, setMessage] = useState(""); // Store current input message
  const [messages, setMessages] = useState([]); // Store the list of messages

  // Handle input change for message
  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  // Handle message submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim() !== "") {
      // Add current user's message
      setMessages([...messages, { text: message, sender: "You" }]);
      setMessage(""); // Clear input field

      const query = message;
      const simple = true;

      try {
        const response = await fetch(
          `http://localhost:8000/agent/${query}?simple=${simple}`
        );
        const data = await response.json();
        console.log(data.messages[data.messages.length - 1].content);

        const last_message = data.messages[data.messages.length - 1].content;
        // Add the response message
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: last_message, sender: "Other" },
        ]);
      } catch (error) {
        console.error("Error:", error);
      }
      //
      // // Simulate "Other" user response with delay
      // setTimeout(() => {
      //   const response = `${data}`; // Automatic response logic
      //   setMessages((prevMessages) => [
      //     ...prevMessages,
      //     { text: response, sender: "Other" },
      //   ]);
      // }, 1000); // Simulate a delay of 1 second for the "Other" user to respond
    }
  };

  //##############################################
  const [ChefActive, setChefActive] = useState(true);
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  function handleChefClick() {
    setChefActive((curr) => !curr);
  }

  return (
    <div className="background">
      <TitleBar
        logoURL="./tempLogo.png"
        title="What's For Dinner?"
        SVG={<ChefSVG state={ChefActive} onClick={handleChefClick} />}
      />
      <div className="main-container">
        <Sidebar title="Pantry">
          <Pantry
            tasks={tasks}
            setTasks={setTasks}
            newTask={newTask}
            setNewTask={setNewTask}
          />
        </Sidebar>
        <RecipeBox />
        <Sidebar
          title="Sous-Chef"
          isActive={ChefActive}
          containerStyle={{ width: "30%" }}
        >
          <Messages
            message={message}
            messages={messages}
            handleInputChange={handleInputChange}
            handleSubmit={handleSubmit}
          />
        </Sidebar>
      </div>
    </div>
  );
}

export default App;
