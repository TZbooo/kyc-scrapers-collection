import { createContext } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ScrapersDataStore from "./context/scrapers";
import Dashboard from "./routes/Dashboard";

const scrapersDataStore = new ScrapersDataStore();
export const ScrapersDataStoreContext = createContext(scrapersDataStore);

const router = createBrowserRouter([
    {
        path: "/",
        element: (
            <ScrapersDataStoreContext.Provider value={scrapersDataStore}>
                <Dashboard />
            </ScrapersDataStoreContext.Provider>
        ),
    },
]);

const App = () => {
    return <RouterProvider router={router} />;
};

export default App;
