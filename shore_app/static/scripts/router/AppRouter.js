import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Header from '../components/Header';
import AddUser from '../components/AddUser';
import UserList from '../components/UserList';
import EditUser from '../components/EditUser';
import SubscriptionList from '../components/SubscriptionList';
import AddSubscription from '../components/AddSubscription';
import EditSubscription from '../components/EditSubscription';


const AppRouter = () => {
  return (
    <BrowserRouter>
      <div>
        <Header />
        <div className="main-content">
          <Switch>
            <Route component={UserList} path="/" exact={true} />
            <Route component={AddUser} path="/user/add" />
            <Route component={AddSubscription} path="/subscription/add" />
            <Route
              render={(props) => (
                <EditUser {...props} />
              )}
              path="/user/edit/:id"
            />
            <Route
              render={(props) => (
                <SubscriptionList {...props} />
              )}
              path="/user/:id/subscriptions"
            />
            <Route
              render={(props) => (
                <EditSubscription {...props} />
              )}
              path="/subscription/edit/:id"
            />
            <Route component={() => <Redirect to="/" />} />
          </Switch>
        </div>
      </div>
    </BrowserRouter>
  );
};

export default AppRouter;
