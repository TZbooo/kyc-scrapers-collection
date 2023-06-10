import PropTypes from "prop-types";
import { useContext } from "react";
import { observer } from "mobx-react-lite";
import { ScrapersDataStoreContext } from "../../App";
import TableItem from "./TableItem";
import { ScraperTypes } from "../../services/scrapers";

const TableContent = observer(({ scraperType }) => {
    const scrapersDataStore = useContext(ScrapersDataStoreContext);

    if (scraperType === ScraperTypes.Telegram) {
        return (
            <>
                {scrapersDataStore.tgScrapersData.map((tableItem) => (
                    <TableItem
                        key={tableItem.object_d}
                        id={tableItem.object_id}
                        name={tableItem.name}
                        total={tableItem.total}
                        totalPerMonth={tableItem.total_per_month}
                        totalPerDay={tableItem.total_per_day}
                        channelLink={tableItem.channel_link}
                        isRunning={tableItem.is_running}
                    />
                ))}
            </>
        );
    }
    if (scraperType === ScraperTypes.WebSite) {
        return (
            <>
                {scrapersDataStore.webSiteScrapersData.map((tableItem) => (
                    <TableItem
                        key={tableItem.object_id}
                        id={tableItem.object_id}
                        name={tableItem.name}
                        total={0}
                        totalPerMonth={0}
                        totalPerDay={0}
                        channelLink={tableItem.channel_link}
                        isRunning={tableItem.is_running}
                    />
                ))}
            </>
        );
    }
});

TableContent.propTypes = {
    scraperType: PropTypes.symbol.isRequired,
};

export default TableContent;
