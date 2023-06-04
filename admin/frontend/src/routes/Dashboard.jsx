import { useContext, useEffect } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../App";
import ScrapersService, { ScraperTypes } from "../api/scrapers";
import BgColumns from "../components/BgColumns";
import Header from "../components/Header";
import ScraperTable from "../components/ScraperTable";

const Dashboard = observer(() => {
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

    const scrapersDataStore = useContext(ScrapersDataStoreContext);

    useEffect(() => {
        const fetchScrapersData = async () => {
            const scraperService = new ScrapersService(ScraperTypes.Tg);
            scrapersDataStore.setTgScrapersData(await scraperService.getList());
        };
        fetchScrapersData();
    }, [scrapersDataStore]);

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
});

export default Dashboard;
