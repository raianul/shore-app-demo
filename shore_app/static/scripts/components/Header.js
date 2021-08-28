import React from 'react';
import { NavLink } from 'react-router-dom';

const Header = () => {
  return (
    <header>
      <h1>Shore Demo App</h1>
      <hr />
      <br />
      <div className="links">
        <NavLink to="/" className="link" activeClassName="active" exact>
          User List
        </NavLink>
        |
        <NavLink to="/user/add" className="link" activeClassName="active">
          Add User
        </NavLink>
        |
        <NavLink to="/subscription/add" className="link" activeClassName="active">
          Add Subscription
        </NavLink>
      </div>
    </header>
  );
};

export default Header;
