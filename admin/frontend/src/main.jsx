import React, { createContext } from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Dashboard from "./routes/Dashboard";
import Register from "./routes/Register";
import Login from "./routes/Login";
import Store from "./context/store";
import "./index.css";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Dashboard />,
    },
    {
        path: "/login",
        element: <Login />,
    },
    {
        path: "/register",
        element: <Register />,
    },
]);

const store = new Store();
export const Context = createContext({ store });

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <Context.Provider value={{ store }}>
            <RouterProvider router={router} />
        </Context.Provider>
    </React.StrictMode>
);
