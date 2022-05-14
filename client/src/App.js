import React from 'react';
// eslint-disable-next-line
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";
import Main from "./pages/Main";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import styled from 'styled-components';

const Div = styled.div`
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

function App() {
  return (
    <Router>
    <Div>
      <Switch>
        <Route exact path="/" component={Main}></Route>
        <Route exact path="/register" component={RegisterPage}></Route>
        <Route exact path="/login" component={LoginPage}></Route>
      </Switch>
    </Div>
  </Router>
  );
}

export default App;
