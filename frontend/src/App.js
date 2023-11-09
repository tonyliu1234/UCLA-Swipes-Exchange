import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import userProfile from "./pages/userProfile";
import signIn from "./pages/signIn";
import signUp from "./pages/signUp";
import changeUserProfile from "./pages/changeUserProfile";
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/userProfile" component={userProfile} />
        <Route path="/signIn" component={signIn} />
        <Route path="/signUp" component={signUp} />
        <Route path="/changeUserProfile" component={changeUserProfile} />
        <Route exact path="/" component={Home} />
      </Switch>
    </Router>
  );
}

export default App;
