import React from "react";
import {
  Box,
  VStack,
  Text,
  Button,
  Flex,
  IconButton,
} from "@chakra-ui/react";
import { Tooltip } from "./ui/tooltip";
import { FiEdit3 } from "react-icons/fi";
import { LuPanelLeftClose } from "react-icons/lu";

function Sidebar({ conversations, onSelect }) {
  return (
    <Box width="250px" bg="#1F1F1F" p={4}>
      <VStack align="stretch" spacing={4}>
        <Flex justifyContent="space-between" alignItems="center">
          <Tooltip
            showArrow
            openDelay={500}
            content="Close Sidebar"
            interactive
            display={{ base: "block", md: "none" }}
          >
            <IconButton
              variant="ghost"
              aria-label="Open Menu"
              bg="transparent"
              _hover={{ bg: "whiteAlpha.300" }}
              _focus={{ bg: "transparent" }}
              size="lg"
            >
              <LuPanelLeftClose color="white" style={{ fontSize: "25px" }} />
            </IconButton>
          </Tooltip>
          <Tooltip
            showArrow
            openDelay={500}
            content="New Chat"
            interactive
            display={{ base: "block", md: "none" }}
          >
            <IconButton
              variant="ghost"
              aria-label="Open Menu"
              color="white"
              bg="transparent"
              _hover={{ bg: "whiteAlpha.300" }}
              _focus={{ bg: "transparent" }}
              size="lg"
            >
              <FiEdit3 color="white" style={{ fontSize: "25px" }} />
            </IconButton>
          </Tooltip>
        </Flex>
        <Text fontWeight="bold" color="white" fontSize="20px">
          Past Conversations
        </Text>
        <Box
          maxHeight="800px"
          overflowY={"auto"}
          css={{
            /* Hide scrollbar track */
            "&::-webkit-scrollbar": {
              width: "6px", // Thin scrollbar
            },
            "&::-webkit-scrollbar-thumb": {
              background: "gray.600", // Scrollbar color
              borderRadius: "10px",
            },
            "&::-webkit-scrollbar-track": {
              background: "transparent", // Hide track
            },
          }}
        >
          {conversations.map((conversation) => (
            <Button
              key={conversation.id}
              onClick={() => onSelect(conversation.id)}
            >
              Conversation {conversation.id}
            </Button>
          ))}
        </Box>
      </VStack>
    </Box>
  );
}

export default Sidebar;
