import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Page1 from './pages/Page1';
import Page2 from './pages/Page2';
import Page3 from './pages/Page3';
import Page4 from './pages/Page4';
import Page5 from './pages/Page5';
import Page6 from './pages/Page6';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Page1} />
        <Route path="/page2" component={Page2} />
        <Route path="/page3" component={Page3} />
        <Route path="/page4" component={Page4} />
        <Route path="/page5" component={Page5} />
        <Route path="/page6" component={Page6} />
      </Switch>
    </Router>
  );
}

export default App;
