import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import userProfile from './pages/userProfile';
import signIn from './pages/signIn';
import signUp from './pages/signUp';
import changeUserProfile from './pages/changeUserProfile';
import AskOrder from './pages/AskOrder';
import BidOrder from './pages/BidOrder';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/userProfile" component={userProfile} />
        <Route path="/signIn" component={signIn} />
        <Route path="/signUp" component={signUp} />
        <Route path="/changeUserProfile" component={changeUserProfile} />
        <Route path="/ask" component={AskOrder} />
        <Route path="/bid" component={BidOrder} />
        <Route exact path="/" component={Home} />
      </Switch>
    </Router>
  );
}

export default App;
