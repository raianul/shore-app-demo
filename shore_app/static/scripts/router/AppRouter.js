import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Header from '../components/Header';
import AddUser from '../components/AddUser';
import UserList from '../components/UserList';
import EditUser from '../components/EditUser';


const AppRouter = () => {
  return (
    <BrowserRouter>
      <div>
        <Header />
        <div className="main-content">
          <Switch>
            <Route component={UserList} path="/" exact={true} />
            <Route component={AddUser} path="/add" />
            <Route
              render={(props) => (
                <EditUser {...props} />
              )}
              path="/edit/:id"
            />
            <Route component={() => <Redirect to="/" />} />
          </Switch>
        </div>
      </div>
    </BrowserRouter>
  );
};

export default AppRouter;
