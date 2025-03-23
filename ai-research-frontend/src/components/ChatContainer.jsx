import React, { useState, useRef, useEffect } from "react";
import { Box, VStack, Textarea } from "@chakra-ui/react";
import ChatMessage from "./ChatMessage";
import useShowToast from "../hooks/useShowToast";
import { v4 as uuid4 } from "uuid";

function ChatContainer({ conversationId, setConversations }) {
  const [messages, setMessages] = useState([]);
  const textAreaRef = useRef(null);
  const [input, setInput] = useState("");
  const chatBottomRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const showToast = useShowToast();

  useEffect(() => {
    textAreaRef.current?.focus();
  }, []);

  useEffect(() => {
    if (chatBottomRef.current) {
      chatBottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    const newMessage = { id: uuid4(), text: message, sender: "user" };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    setLoading(true);

    // Add a skeleton message immediately
    setMessages((prev) => [...prev, { id: "loading", sender: "llm", text: "" }]);

    try {
      const response = await fetch("/api/basic-research/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
          conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const llmResponse = await response.json();

      setTimeout(() => {
        // Replace the skeleton message with the actual response
        setMessages((prev) => {
          const updatedMessages = prev.filter((msg) => msg.id !== "loading");
          return [
            ...updatedMessages,
            {
              id: uuid4(),
              text: llmResponse.text,
              sender: "llm",
              charts: llmResponse.charts,
              links: llmResponse.links,
              related_questions: llmResponse.related_questions || [],
            },
          ];
        });
        setLoading(false);
      }, 3000);

      if (conversationId == null) {
        setConversations((prev) => [
          ...prev,
          { id: llmResponse.conversationId },
        ]);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      showToast("Error", error.message, "error");
      // Remove the loading message if there is an error
      setMessages((prev) => prev.filter((msg) => msg.id !== "loading"))
      setLoading(false);
    }
  };

  const handleRelatedQuestionClick = (question) => {
    handleSendMessage(question);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(input);
    }
  };

  return (
    <VStack spacing={0} height="100vh" align="stretch">
      <Box
        flex="1"
        overflowY="auto"
        p={4}
        bg="#2A2A2A"
        maxHeight="calc(100vh - 150px)"
        css={{
          "&::-webkit-scrollbar": {
            width: "6px",
          },
          "&::-webkit-scrollbar-thumb": {
            background: "gray.600",
            borderRadius: "10px",
          },
          "&::-webkit-scrollbar-track": {
            background: "transparent",
          },
        }}
      >
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            onRelatedQuestionClick={handleRelatedQuestionClick}
            loading={message.id === "loading" && loading}
          />
        ))}
        <div ref={chatBottomRef} />
      </Box>
      <Box bg="blackAlpha600" position="sticky" bottom="0">
        <Textarea
          ref={textAreaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask Northstar Co-Pilot"
          size="lg"
          bg="blackAlpha.600"
          color="white"
        />
      </Box>
    </VStack>
  );
}

export default ChatContainer;