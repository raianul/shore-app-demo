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
        &nbsp;
        <NavLink to="/add" className="link" activeClassName="active">
          Add User
        </NavLink>
      </div>
    </header>
  );
};

export default Header;
