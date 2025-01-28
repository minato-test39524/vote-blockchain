import { Button, List, ListItem, ListItemText } from "@mui/material";
import axios from "axios";
import { useState } from "react";


export const Total = () => {
    const [ totalData, setTotalData ] = useState([]);

    const onClickShowTotal = () => {
        axios.get(`http://localhost:8000/num-of-votes`)
        .then(res => {
            console.log(res.data);
            setTotalData(res.data);
        })
        .catch(error => {
            console.log(error);
        });
    }


    return (
        <div style={{ border: "solid, lightsteelblue", borderRadius: "10px", height: "400px", width: "350px", backgroundColor: "aliceblue", padding: "8px", marginLeft: "16px", marginTop: "8px"}} >
            <Button variant="outlined" onClick={onClickShowTotal}>Show Total</Button>
            <List>
                {Object.entries(totalData).map(([key, value]) => ( 
                    <ListItem key={key}>
                        <ListItemText>候補者ID {key}: {value} 票</ListItemText>
                    </ListItem>
                ))}
            </List>
        </div>
    )
}