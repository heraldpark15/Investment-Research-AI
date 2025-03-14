import React from 'react'
import StockDisplay from '../components/Displays/StockDisplay'
import { Box, Container, Flex} from '@chakra-ui/react'

const HomePage = () => {
    return (
        <Container maxW={"container.lg"}>
            <StockDisplay />
        </Container>
    )
}

export default HomePage