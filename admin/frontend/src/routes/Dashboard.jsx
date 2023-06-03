import BgColumns from "../components/BgColumns";
import Header from "../components/Header";
import ScraperList from "../components/ScraperTable";

const Dashboard = () => {
    return (
        <>
            <BgColumns />
            <Header />
            <ScraperList name="Телеграм каналы" />
        </>
    );
};

export default Dashboard;
