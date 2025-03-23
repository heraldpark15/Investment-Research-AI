import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import { Box, Link, VStack, Button, HStack, Skeleton, Flex } from "@chakra-ui/react";
import useShowToast from "../hooks/useShowToast";
import { HiChevronDoubleRight } from "react-icons/hi";

function ChatMessage({ message, onRelatedQuestionClick, loading }) {
  const showToast = useShowToast();
  const [displayedText, setDisplayedText] = useState("");
  const [typing, setTyping] = useState(false);
  const textRef = useRef(message.text);

  useEffect(() => {
    if (message.sender === "llm" && message.text) {
      setDisplayedText("");
      setTyping(true);
      let charIndex = 0;
      const interval = setInterval(() => {
        if (charIndex < message.text.length) {
          setDisplayedText((prev) => prev + message.text.charAt(charIndex));
          charIndex++;
        } else {
          clearInterval(interval);
          setTyping(false);
        }
      }, 20); // Adjust typing speed (lower is faster)
      return () => clearInterval(interval);
    } else {
      setDisplayedText(message.text);
    }
  }, [message.text, message.sender]);
  let relatedQuestions = [];

  if (typeof message.related_questions === "string") {
    try {
      relatedQuestions = JSON.parse(message.related_questions);
    } catch (error) {
      showToast("Error", "Error parsing related_questions", "error");
      relatedQuestions = [];
    }
  } else if (Array.isArray(message.related_questions)) {
    relatedQuestions = message.related_questions;
  }

  return (
    <Box
      display="flex"
      justifyContent={message.sender === "user" ? "flex-end" : "flex-start"}
      mb={2}
    >
      <Box
        bg={message.sender === "user" ? "gray.700" : ""}
        p={3}
        borderRadius="4xl"
        maxW="80%"
      >
        <Box color="white">
          {loading ? (
            <ResponseSkeleton/>
          ) : (
            <ReactMarkdown>{message.text}</ReactMarkdown>
          )}
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

          {relatedQuestions.length > 0 && !loading && (
            <VStack mt={3} align="start">
              <Box fontWeight="bold">Related Questions</Box>
              {relatedQuestions.map((question, index) => (
                <Button
                  key={index}
                  variant="link"
                  colorScheme="blue"
                  onClick={() => {
                    onRelatedQuestionClick(question);
                  }}
                  _hover={{
                    color: "gray.400",
                    "& svg": { transform: "translateX(10px)" },
                  }}
                >
                  <HStack spacing={10}>
                    <ReactMarkdown>{question}</ReactMarkdown>
                    <HiChevronDoubleRight
                      style={{ transition: "transform 0.2s ease-in-out" }}
                    />
                  </HStack>
                </Button>
              ))}
            </VStack>
          )}
        </Box>
      </Box>
    </Box>
  );
}

export default ChatMessage;


const ResponseSkeleton = () => {
  return (
    <Flex
      gap={{ base: 4, sm: 10}}
      py={10}
      direction={{ base: "column", sm: "row"}}
      justifyContent={"center"}
      alignItems={"center"}
    >
      <VStack alignItems={{ base: "center", sm: "flex-start"}} gap={2} mx={"auto"} flex={1}>
        <Skeleton height='12px' width='150px' />
        <Skeleton height='12px' width='100px' />
      </VStack>
    </Flex>
  )
}