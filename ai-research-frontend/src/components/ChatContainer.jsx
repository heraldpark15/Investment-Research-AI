import React, { useState, useRef, useEffect } from 'react';
import { Box, VStack, Textarea, Button } from '@chakra-ui/react';
import ChatMessage from './ChatMessage';
import useShowToast from '../hooks/useShowToast';

function ChatContainer({ conversationId, setConversations }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatBottomRef = useRef(null);
  const showToast = useShowToast();

  useEffect(() => {
    if (chatBottomRef.current) {
      chatBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { text: input, sender: 'user' };
    setMessages((prev) => [...prev, newMessage]);
    setInput('');

    try {
      const response = await fetch('/api/basic-research/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          conversationId: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const llmResponse = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          text: llmResponse.text,
          sender: 'llm',
          charts: llmResponse.charts,
          links: llmResponse.links,
        },
      ]);

      if (conversationId == null) {
        setConversations((prev) => [...prev, { id: llmResponse.conversationId }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      showToast('Error', error.message, 'error'); 
    }
  };

  return (
    <VStack spacing={4} height="100%" align="stretch">
      <Box flex="1" overflowY="auto" p={4}>
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
        <div ref={chatBottomRef} />
      </Box>
      <Textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        size="lg"
      />
      <Button colorScheme="blue" onClick={handleSendMessage}>
        Send
      </Button>
    </VStack>
  );
}

export default ChatContainer;