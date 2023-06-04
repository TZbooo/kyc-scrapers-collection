import PropTypes from "prop-types";
import { useContext } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../../App";
import ScrapersService, { ScraperTypes } from "../../../services/scrapers";
import Form from "../Form";

const TelegramScraperToggleRunningStatusAllForm = observer(
    ({ disable, disableSetter }) => {
        const scrapersDataStore = useContext(ScrapersDataStoreContext);
        const runningScrapers = scrapersDataStore.tgScrapersData.filter(
            (scraper) => scraper.isRunning
        );

        const handleSubmit = async (event) => {
            event.preventDefault();
            const scrapersService = new ScrapersService(ScraperTypes.Telegram);

            Promise.all(
                runningScrapers.map(
                    async (scraper) => {
                        await scrapersService.setRunningStatus(
                            scraper.id,
                            false
                        )
                        scraper.isRunning = false;
                    }
                )
            );
            disableSetter(true);
        };

        return (
            <>
                <Form
                    header='Вы действительно хотите остановить все запущенные парсеры'
                    buttonText='Остановить'
                    handleSubmit={handleSubmit}
                    disable={disable}
                    disableSetter={disableSetter}
                ></Form>
            </>
        );
    }
);

TelegramScraperToggleRunningStatusAllForm.propTypes = {
    disable: PropTypes.bool.isRequired,
    disableSetter: PropTypes.func.isRequired,
};

export default TelegramScraperToggleRunningStatusAllForm;
