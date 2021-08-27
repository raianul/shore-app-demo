import React from "react";
import ReactDOM from "react-dom";
import HelloWorld from "./HelloWorld";
import User from "./User";

ReactDOM.render(<HelloWorld />, document.getElementById("react-root"));
ReactDOM.render(<User />, document.getElementById("user-list"));
