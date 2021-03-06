<products>
    {
        for $product in fn:doc("q1b.xml")/db/products/row
        return
            <product pid="{$product/pid}">
            {$product/name}{$product/price}{$product/description}
            {
                for $store in fn:doc("q1b.xml")/db/stores/row
                for $sell in fn:doc("q1b.xml")/db/sells/row
                where $product/pid = $sell/pid and $store/sid = $sell/sid
                return
                <store sid="{$store/sid}">
                    {$store/name}{$store/phones}{$sell/markup}
                </store>

            }
        </product>
    }
</products>