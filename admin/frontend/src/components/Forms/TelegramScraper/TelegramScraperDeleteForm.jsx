import PropTypes from "prop-types";
import { useContext } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../../App";
import ScrapersService, { ScraperTypes } from "../../../services/scrapers";
import Form from "../Form";

const TelegramScraperDeleteForm = observer(
    ({ telegramScraperId, disable, disableSetter }) => {
        const scrapersDataStore = useContext(ScrapersDataStoreContext);

        const handleSubmit = async (event) => {
            event.preventDefault();
            console.log(telegramScraperId);
            const scrapersService = new ScrapersService(ScraperTypes.Telegram);
            await scrapersService.deleteScraper(telegramScraperId);
            disableSetter(true);
            scrapersDataStore.tgScrapersData =
                scrapersDataStore.tgScrapersData.filter(
                    (scraper) => scraper.object_id !== telegramScraperId
                );
        };

        return (
            <>
                <Form
                    header='Вы действительно хотите удалить парсер?'
                    buttonText='Удалить'
                    handleSubmit={handleSubmit}
                    disable={disable}
                    disableSetter={disableSetter}
                >
                    <input
                        type='hidden'
                        value={telegramScraperId}
                        name='telegram_scraper_id'
                    />
                </Form>
            </>
        );
    }
);

TelegramScraperDeleteForm.propTypes = {
    telegramScraperId: PropTypes.string.isRequired,
    disable: PropTypes.bool.isRequired,
    disableSetter: PropTypes.func.isRequired,
};

export default TelegramScraperDeleteForm;
