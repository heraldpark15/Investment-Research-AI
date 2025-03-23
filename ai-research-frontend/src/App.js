import React from "react";
import { Route, Routes } from "react-router";
import Chat from "./Pages/Chat";
import HomePage from "./Pages/HomePage";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage/>} />
        <Route path="/chat" element={<Chat/>} />
      </Routes>
    </>
  );
}

export default App;
