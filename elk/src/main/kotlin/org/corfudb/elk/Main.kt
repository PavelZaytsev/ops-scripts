package org.corfudb.elk

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.arguments.argument
import java.nio.file.Paths

fun main(args : Array<String>) {
    require(args.isNotEmpty()) { "empty parameters" }

    println("Start processing! Parameters: ${args.joinToString()}")

    Processing().main(args)
}

class Processing : CliktCommand() {
    private val bug: String by argument(help = "bug")
    private val bundle: String by argument(help = "bundle")
    private val url: String by argument(help = "support bundle url")

    override fun run() {
        val supportBundleManager = SupportBundleManager()
        val dataDir = Paths.get("build", "data", bug)

        dataDir.toFile().mkdirs();

        supportBundleManager.download(url, dataDir.resolve("$bundle.tgz"))
    }
}

