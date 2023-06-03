import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { observer } from "mobx-react-lite";
import { Context } from "../App";
import BgColumns from "../components/BgColumns";
import Header from "../components/Header";

const Dashboard = observer(() => {
    const { store } = useContext(Context);
    const navigate = useNavigate();

    useEffect(() => {
        const checkAuth = async () => {
            await store.checkAuth();

            if (!store.isAuth) {
                navigate("/login");
            }
        };
        checkAuth();
    }, [store, navigate]);

    return (
        <>
            <BgColumns />
            <Header />
        </>
    );
});

export default Dashboard;
