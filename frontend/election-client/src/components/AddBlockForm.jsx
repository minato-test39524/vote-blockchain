import { Box, Button, Card, CardContent, Typography } from "@mui/material";
import axios from "axios";
import { useState } from "react";


export const AddBlockForm = () => {
    const [ addResult, setAddResult ] = useState()

    const onClickAdd = () => {
        axios.get(`http://localhost:8000/block`)
        .then(res => {
            console.log(JSON.stringify(res.data));
            setAddResult(JSON.stringify(res.data, null, 2));
        })
        .catch(error => {
            console.log(error)
        });
    }


    return (
        <div style={{ border: "solid, lightsteelblue", borderRadius: "10px", height: "400px", width: "820px", backgroundColor: "aliceblue", padding: "8px", marginLeft: "8px"}} >
            <Button variant="outlined" onClick={onClickAdd}>Add Block</Button>
            <Card sx={{ marginTop: "8px" }}>
                <CardContent>
                    <Box
                        sx={{
                            maxHeight: "400px",
                            maxWidth: "100%",
                            overflow: "auto",
                            '& pre': {
                                margin: 0,
                                whiteSpace: "pre",
                                wordBreak: "break-word"
                            }
                        }}
                    >
                        <Typography component="pre">
                            {addResult}
                        </Typography>
                    </Box>
                </CardContent>
            </Card>
        </div>
    )
}