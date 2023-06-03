import { createContext } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Dashboard from "./routes/Dashboard";
import Register from "./routes/Register";
import Login from "./routes/Login";
import Store from "./context/store";

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

const App = () => {
    return (
        <Context.Provider value={{ store }}>
            <RouterProvider router={router} />
        </Context.Provider>
    );
};

export default App;
