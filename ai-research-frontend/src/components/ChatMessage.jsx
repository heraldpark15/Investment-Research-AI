import React from 'react';
import ReactMarkdown from 'react-markdown'
import { Box, Link, VStack } from '@chakra-ui/react';

function ChatMessage({ message }) {
  return (
    <Box alignSelf={message.sender === 'user' ? 'flex-end' : 'flex-start'} mb={2}>
      <Box
        bg={message.sender === 'user' ? 'blue.100' : 'gray.100'}
        p={3}
        borderRadius="md"
      >
        <ReactMarkdown>{message.text}</ReactMarkdown>
        {message.charts && message.charts.length > 0 && (
          <VStack>
            {/* {message.charts.map((chart, index) => (
              <ChartDisplay key={index} data={chart.data} type={chart.type} />
            ))} */}
          </VStack>
        )}
        {message.links && message.links.length > 0 && (
          <VStack>
            {message.links.map((link, index) => (
              <Link key={index} href={link} isExternal>
                {link}
              </Link>
            ))}
          </VStack>
        )}
      </Box>
    </Box>
  );
}

export default ChatMessage;