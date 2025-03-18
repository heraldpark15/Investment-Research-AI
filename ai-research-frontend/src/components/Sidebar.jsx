import React from 'react';
import { Box, VStack, Text, Button } from '@chakra-ui/react';

function Sidebar({ conversations, onSelect }) {
  return (
    <Box width="250px" bg="gray.100" p={4}>
      <VStack align="stretch" spacing={4}>
        <Text fontWeight="bold">Past Conversations</Text>
        {conversations.map((conversation) => (
          <Button
            key={conversation.id}
            onClick={() => onSelect(conversation.id)}
          >
            Conversation {conversation.id}
          </Button>
        ))}
      </VStack>
    </Box>
  );
}

export default Sidebar;