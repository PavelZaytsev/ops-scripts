package org.corfudb.elk

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.arguments.argument
import java.nio.file.Paths

fun main(args : Array<String>) {
    if(args.isEmpty()){
        throw IllegalArgumentException("empty parameters")
    }

    println("Start processing! Parameters: ${args.joinToString()}")

    Processing().main(args)
}

class Processing : CliktCommand() {
    private val bug: String by argument(help = "bug")
    private val url: String by argument(help = "support bundle url")

    override fun run() {
        val supportBundleManager = SupportBundleManager()
        supportBundleManager.download(url, Paths.get("build", "data", "$bug.tgz"))
    }
}

