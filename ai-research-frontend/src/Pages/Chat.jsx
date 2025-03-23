import React, { useState } from "react";
import { Box, Flex } from "@chakra-ui/react";
import Sidebar from "../components/Sidebar";
import ChatContainer from "../components/ChatContainer";
import RightSidebar from "../components/RightSidebar";

const Chat = () => {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);

  const handleConversationSelect = (conversationId) => {
    setCurrentConversation(conversationId);
  };
  return (
    <Flex height="100vh" width="100vw" bg="#1F1F1F">
      <RightSidebar top="15px" right="20px" />
      <Sidebar
        conversations={conversations}
        onSelect={handleConversationSelect}
      />
      <Box flex="1" display="flex" flexDirection="column">
        <Box bg="#2A2A2A" p={4} boxShadow="md" height="50px">
          {/* Header Box Content */}
        </Box>
        <ChatContainer
          conversationId={currentConversation}
          setConversations={setConversations}
        />
      </Box>
    </Flex>
  );
};

export default Chat;
