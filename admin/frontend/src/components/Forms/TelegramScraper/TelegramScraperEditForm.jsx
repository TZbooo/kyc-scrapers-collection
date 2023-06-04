import PropTypes from "prop-types";
import { useContext, useEffect, useState } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../../App";
import ScrapersService, { ScraperTypes } from "../../../services/scrapers";
import Form from "../Form";
import TextInput from "../TextInput";
import Checkbox from "../Checkbox";

const TelegramScraperEditForm = observer(
    ({ telegramScraperId, disable, disableSetter }) => {
        const scrapersDataStore = useContext(ScrapersDataStoreContext);
        const scraper = scrapersDataStore.tgScrapersData.find(
            (scraper) => scraper.id === telegramScraperId
        );

        const [name, setName] = useState(scraper.name);

        const [scraperOrigin, setScraperOrigin] = useState(scraper.origin);
        const [scraperOriginError, setScraperOriginError] = useState("");

        const [offset, setOffset] = useState(scraper.offset);
        const [offsetError, setOffsetError] = useState("");

        const [limit, setLimit] = useState(scraper.limit);
        const [limitError, setLimitError] = useState("");

        const [minCharacters, setMinCharacters] = useState(
            scraper.minCharacters
        );
        const [minCharactersError, setMinCharactersError] = useState("");

        const [collectRetro, setCollectRetro] = useState(scraper.collectRetro);

        const handleSubmit = async (event) => {
            event.preventDefault();
            const scrapersService = new ScrapersService(ScraperTypes.Telegram);
            const response = await scrapersService.updateScraper(
                telegramScraperId,
                name,
                minCharacters,
                offset,
                limit,
                scraperOrigin,
                collectRetro
            );
            disableSetter(true);
            scraper.name = response.name;
            scraper.minCharacters = response.minCharacters;
            scraper.offset = response.offset;
            scraper.limit = response.limit;
            scraper.origin = response.origin;
            scraper.collectRetro = response.collectRetro;
        };

        useEffect(() => {
            setScraperOriginError(validateChannelLink(scraperOrigin));
            setOffsetError(validatePositiveNumberInput(offset));
            setLimitError(validatePositiveNumberInput(limit));
            setMinCharactersError(validatePositiveNumberInput(minCharacters));
        }, [scraperOrigin, offset, limit, minCharacters]);

        return (
            <>
                <Form
                    header='Изменить парсер'
                    buttonText='Сохранить и перезапустить'
                    handleSubmit={handleSubmit}
                    disable={disable}
                    disableSetter={disableSetter}
                >
                    <input
                        type='hidden'
                        value={telegramScraperId}
                        name='telegram_scraper_id'
                    />
                    <TextInput
                        placeholder='Имя'
                        value={name}
                        valueSetter={setName}
                    />
                    <TextInput
                        placeholder='Ссылка на канал'
                        value={scraperOrigin}
                        valueSetter={setScraperOrigin}
                        error={scraperOriginError}
                    />
                    <TextInput
                        placeholder='Оффсет'
                        value={offset}
                        valueSetter={setOffset}
                        error={offsetError}
                    />
                    <TextInput
                        placeholder='Лимит'
                        value={limit}
                        valueSetter={setLimit}
                        error={limitError}
                        required={false}
                    />
                    <TextInput
                        placeholder='Минимальное количество символов'
                        value={minCharacters}
                        valueSetter={setMinCharacters}
                        error={minCharactersError}
                    />
                    <Checkbox
                        placeholder='Ретроспектива'
                        checked={collectRetro}
                        checkedSetter={setCollectRetro}
                    />
                </Form>
            </>
        );
    }
);

TelegramScraperEditForm.propTypes = {
    telegramScraperId: PropTypes.string.isRequired,
    disable: PropTypes.bool.isRequired,
    disableSetter: PropTypes.func.isRequired,
};

const validateChannelLink = (channelLink) => {
    const channelLinkMustStartWith = "https://t.me/";

    if (
        channelLinkMustStartWith.slice(0, channelLink.length) !==
        channelLink.slice(0, channelLinkMustStartWith.length)
    ) {
        return "Ссылка на канал должна начинаться с https://t.me/";
    } else {
        return false;
    }
};

const validatePositiveNumberInput = (value) => {
    if (!value) {
        return false;
    }

    if (isNaN(parseInt(value))) {
        return "Поле должно быть числом";
    }

    if (parseInt(value) < 0) {
        return "Поле должно быть больше нуля";
    }
};

export default TelegramScraperEditForm;
