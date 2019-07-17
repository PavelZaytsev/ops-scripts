package org.corfudb.elk

import java.net.URL
import java.nio.channels.Channels
import java.nio.channels.FileChannel
import java.nio.file.Path
import java.nio.file.StandardOpenOption
import java.util.*

class SupportBundleManager {

    fun download(url: String, directory: Path) {
        println("Download support bundle: $url")

        val bundleChannel = Channels.newChannel(URL(url).openStream())

        val options = EnumSet.of(
                StandardOpenOption.READ,
                StandardOpenOption.WRITE,
                StandardOpenOption.CREATE_NEW
        )
        val bundleFile = FileChannel.open(directory, options)
        bundleFile.transferFrom(bundleChannel, 0, Long.MAX_VALUE)
        bundleFile.close()


    }
}