import BgColumns from "../components/BgColumns";
import Header from "../components/Header";
import ScraperTable from "../components/ScraperTable";

const Dashboard = () => {
    return (
        <>
            <BgColumns />
            <Header />
            <ScraperTable name="Телеграм каналы" />
        </>
    );
};

export default Dashboard;
