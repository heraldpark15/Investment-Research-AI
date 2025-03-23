import React from "react";
import { Box, Text, VStack, Button, Link } from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";
import RightSidebar from "../components/RightSidebar";

const HomePage = () => {
  return (
    <Box position="relative" w="100vw" h="100vh" overflow="hidden">
      <Box position="absolute" top="0" left="0" w="100%" h="100%" zIndex="-1">
        <video
          autoPlay
          loop
          muted
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        >
          <source src="/background.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </Box>

      <RightSidebar top="15px" right="20px" />

      <VStack
        position="absolute"
        top="50%"
        left="50%"
        transform="translate(-50%, -50%)"
        textAlign="center"
        color="white"
        spacing={6}
      >
        <Text
          fontSize="5xl"
          fontWeight="bold"
          textShadow="2px 2px 10px rgba(0, 0, 0, 0.7)"
        >
          Northstar Co-Pilot
        </Text>
        <Text fontSize="2xl" textShadow="2px 2px 10px rgba(0, 0, 0, 0.7)">
          Leveraging AI for next-generation investment research
        </Text>
        <Link to={"/chat"} as={RouterLink}>
          <Button
            variant="outline"
            borderRadius="full"
            px={8}
            py={6}
            fontSize="lg"
            fontWeight="bold"
            color="white"
            borderColor="white"
            _hover={{
              bg: "white",
              color: "black",
              transform: "scale(1.05)",
              transition: "all 0.3s ease-in-out",
            }}
          >
            Get Started
          </Button>
        </Link>
      </VStack>
    </Box>
  );
};

export default HomePage;
