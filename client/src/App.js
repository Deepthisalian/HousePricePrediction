
import React, {useState, useEffect} from 'react'
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import { FormGroup, TextField, withTheme } from '@mui/material';
import Button from '@mui/material/Button';

function App () {
  const [value, setValue] = React.useState('1');
     var result = ""
    const [input, setInput] = useState([{}])
    const [data, satData] = useState("")
    const submit = e => {
        e.preventDefault()
        console.log(input)
        fetch("http://localhost:5000/members",{
          method: "POST",
          body: JSON.stringify(input)
        }).then(
                 res => res.json()
          ).then(
          data => {
            satData(data)
            result = data 
            console.log(typeof(result))
          }

        )
    }
    const handleChange = (event) => {
      setValue(event.target.value);
    };
    {
      const myStyle={
        backgroundImage: "url(/blue.jpg)",
        height:'100vh',
        fontSize:'20px',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        color: withTheme,   
};

const head={
  fontSize: '30px',
  color: withTheme,
};

  return (
    
    <div style={myStyle}>
      
      <React.Fragment>
      <CssBaseline />
    <Container align='center' maxWidth="lg">
    <FormGroup  >
    <form onSubmit={submit}>
    <label style={head} >Bangalore House Price Prediction</label><br></br><br></br>

    <label className='center'>Location</label><br></br>
      <TextField
        id = "filled-basic"
        label="Location"
        variant = "filled"
        type="text"
        name="input[area]"
        value={input.area}
        onChange={e => setInput({ ...input, area: e.target.value })}
      /><br></br><br></br>
       
    <label>Squarefeet</label><br></br>
    <TextField
        id = "filled-basic"
        label="Squarefeet"
        variant = "filled"
        type="text"
        name="input[bhk]"
        value={input.bhk}
        onChange={e => setInput({ ...input, bhk: e.target.value })}
      /><br></br><br></br>
      

      <label>Bathrooms</label><br></br>
      <TextField
        id = "filled-basic"
        label="Bathrooms"
        variant = "filled"
        type="text"
        name="input[bath]"
        value={input.bath}
        onChange={e => setInput({ ...input, bath: e.target.value })}
      /><br></br><br></br>

<label>Bedrooms</label><br></br>

<TextField
        id = "filled-basic"
        label="Bedrooms"
        variant = "filled"
        type="text"
        name="input[loc]"
        value={input.loc}
        onChange={e => setInput({ ...input, loc: e.target.value })}
      /><br></br>

      <br></br>
      <Button variant="contained" type="submit" name="Predict" align='center'>Predict</Button>
    </form>
    </FormGroup>
    {data + "Crores"}
  
    </Container>
    </React.Fragment>
    </div>
  )

  
}}

export default App;