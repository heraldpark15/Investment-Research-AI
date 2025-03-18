import React, { useState } from 'react';
import { Box, Flex } from '@chakra-ui/react';
import Sidebar from './components/Sidebar';
import ChatContainer from './components/ChatContainer';

function App() {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);

  const handleConversationSelect = (conversationId) => {
    setCurrentConversation(conversationId);
  };

  return (
    <Flex height="100vh">
      <Sidebar
        conversations={conversations}
        onSelect={handleConversationSelect}
      />
      <Box flex="1" p={4}>
        <ChatContainer
          conversationId={currentConversation}
          setConversations={setConversations}
        />
      </Box>
    </Flex>
  );
}

export default App;