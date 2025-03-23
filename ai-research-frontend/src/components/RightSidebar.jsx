import React, { useState } from "react";
import { Text, IconButton, Icon, Stack } from "@chakra-ui/react";
import { FiAlignJustify } from "react-icons/fi";
import { motion } from "framer-motion";
import { IoClose } from "react-icons/io5";

const RightSidebar = ({ top, right }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isExiting, setIsExiting] = useState(false);

  const handleDialogToggle = () => {
    if (isOpen) {
      setIsExiting(true);
      setTimeout(() => {
        setIsOpen(false);
        setIsExiting(false);
      }, 0);
    } else {
      setIsOpen(true);
    }
  };

  return (
    <>
      {!isOpen && (
        <IconButton
          aria-label="Open Menu"
          variant="ghost"
          color="white"
          position="absolute"
          top={top}
          right={right}
          _hover={{ bg: "whiteAlpha.300" }}
          size="lg"
          onClick={handleDialogToggle}
        >
          <Icon as={FiAlignJustify} boxSize={8} />
        </IconButton>
      )}

      {(isOpen || isExiting) && (
        <motion.div
          initial={{ x: "100%" }}
          animate={{ x: isOpen ? 0 : "100px" }}
          exit={{ x: "100%" }}
          transition={{
            type: "spring",
            stiffness: 200,
            damping: 30,
          }}
          style={{
            position: "absolute",
            top: "0",
            right: "0",
            width: "250px",
            height: "100%",
            backgroundColor: "white",
            zIndex: "1000",
            padding: "20px",
            boxShadow: "2px 0px 10px rgba(0, 0, 0, 0.1)",
            borderRight: "1px solid #ddd",
          }}
        >
          <Stack spacing={4} direction="row" alignItems="flex-start">
            <IconButton
              position="absolute"
              top="13px"
              right="20px"
              onClick={handleDialogToggle}
              color="white"
              backgroundColor="transparent"
              _hover={{
                bg: "grey",
              }}
            >
              <IoClose color="black" />
            </IconButton>
            <Stack spacing={3}>
              <Text color="black" cursor="pointer">
                Signup/Login
              </Text>
              <Text color="black" cursor="pointer">
                About
              </Text>
              <Text color="black" cursor="pointer">
                Source
              </Text>
            </Stack>
          </Stack>
        </motion.div>
      )}
    </>
  );
};

export default RightSidebar;
