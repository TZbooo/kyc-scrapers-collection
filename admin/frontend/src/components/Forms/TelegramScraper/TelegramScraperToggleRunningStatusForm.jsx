import PropTypes from "prop-types";
import { useContext } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../../App";
import ScrapersService, { ScraperTypes } from "../../../services/scrapers";
import Form from "../Form";

const TelegramScraperToggleRunningStatusForm = observer(
    ({ telegramScraperId, disable, disableSetter }) => {
        const scrapersDataStore = useContext(ScrapersDataStoreContext);
        const scraper = scrapersDataStore.tgScrapersData.find(
            (scraper) => scraper.object_id === telegramScraperId
        );

        const handleSubmit = async (event) => {
            event.preventDefault();
            const scrapersService = new ScrapersService(ScraperTypes.Telegram);
            const currentRunningStatus = await scrapersService.setRunningStatus(
                telegramScraperId,
                !scraper.is_running
            );
            scraper.is_running = currentRunningStatus;
            disableSetter(true);
        };

        return (
            <>
                <Form
                    header={
                        scraper.is_running
                            ? "Вы действительно хотите остановить парсер"
                            : "Вы действительно хотите запустить парсер"
                    }
                    buttonText={scraper.is_running ? "Остановить" : "Запустить"}
                    handleSubmit={handleSubmit}
                    disable={disable}
                    disableSetter={disableSetter}
                ></Form>
            </>
        );
    }
);

TelegramScraperToggleRunningStatusForm.propTypes = {
    telegramScraperId: PropTypes.string.isRequired,
    disable: PropTypes.bool.isRequired,
    disableSetter: PropTypes.func.isRequired,
};

export default TelegramScraperToggleRunningStatusForm;
