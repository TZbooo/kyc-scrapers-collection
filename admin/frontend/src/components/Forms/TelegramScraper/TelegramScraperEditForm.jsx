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
            (scraper) => scraper.object_id === telegramScraperId
        );

        const [name, setName] = useState(scraper.name);

        const [channelLink, setChannelLink] = useState(scraper.channel_link);
        const [channelLinkError, setChannelLinkError] = useState("");

        const [offset, setOffset] = useState(scraper.offset);
        const [offsetError, setOffsetError] = useState("");

        const [limit, setLimit] = useState(scraper.limit);
        const [limitError, setLimitError] = useState("");

        const [minCharacters, setMinCharacters] = useState(
            scraper.min_characters
        );
        const [minCharactersError, setMinCharactersError] = useState("");

        const [reverse, setReverse] = useState(scraper.reverse);

        const handleSubmit = async (event) => {
            event.preventDefault();
            const scrapersService = new ScrapersService(ScraperTypes.Telegram);
            const response = await scrapersService.updateScraper(
                telegramScraperId,
                name,
                minCharacters,
                offset,
                limit ? limit : null,
                channelLink,
                reverse
            );
            disableSetter(true);
            scraper.name = response.name;
            scraper.min_characters = response.min_characters;
            scraper.offset = response.offset;
            scraper.limit = response.limit;
            scraper.channel_link = response.channel_link;
            scraper.reverse = response.reverse;
        };

        useEffect(() => {
            setChannelLinkError(validateChannelLink(channelLink));
            setOffsetError(validatePositiveNumberInput(offset));
            setLimitError(validatePositiveNumberInput(limit));
            setMinCharactersError(validatePositiveNumberInput(minCharacters));
        }, [channelLink, offset, limit, minCharacters]);

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
                        value={channelLink}
                        valueSetter={setChannelLink}
                        error={channelLinkError}
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
                        checked={reverse}
                        checkedSetter={setReverse}
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
