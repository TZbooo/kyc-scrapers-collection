import BgColumns from "../components/BgColumns";
import Header from "../components/Header";
import ScraperTable from "../components/ScraperTable";

const Dashboard = () => {
    const telegramChannelTableHeaders = [
        {
            id: 0,
            name: "Телеграм каналы",
        },
        {
            id: 1,
            name: "Всего взаимодействий",
        },
        {
            id: 2,
            name: "За месяц взаимодействий",
        },
        {
            id: 3,
            name: "За сегодня взаимодествий",
        },
        {
            id: 4,
            name: "Информационный источник",
        },
        {
            id: 5,
            name: "Запуск",
        },
    ];

    return (
        <>
            <BgColumns />
            <Header />
            <ScraperTable
                name='Телеграм каналы'
                headers={telegramChannelTableHeaders}
            />
        </>
    );
};

export default Dashboard;
