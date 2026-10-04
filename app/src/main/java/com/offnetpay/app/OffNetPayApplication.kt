package com.offnetpay.app

import android.app.Application
import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import com.offnetpay.app.data.AppDatabase
import com.offnetpay.app.data.HistoryRepository
import com.offnetpay.app.data.PreferencesRepository
import com.offnetpay.app.domain.ActionRunner
import com.offnetpay.app.platform.CarrierDetector
import com.offnetpay.app.platform.OverlayControllerImpl
import com.offnetpay.app.platform.QrScannerManager
import com.offnetpay.app.platform.UssdEngine

/**
 * Top-level DataStore delegate (must be at file level per DataStore docs).
 */
private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

/**
 * Application class wiring all singleton dependencies via manual DI.
 *
 * Validates: Requirements 14.1, 14.2, 15.1
 */
class OffNetPayApplication : Application() {

    // ─── Data Layer ────────────────────────────────────────────────────────────

    lateinit var database: AppDatabase
        private set

    lateinit var historyRepo: HistoryRepository
        private set

    lateinit var prefsRepo: PreferencesRepository
        private set

    // ─── Platform Layer ────────────────────────────────────────────────────────

    lateinit var overlayController: OverlayControllerImpl
        private set

    lateinit var ussdEngine: UssdEngine
        private set

    lateinit var carrierDetector: CarrierDetector
        private set

    lateinit var qrScannerManager: QrScannerManager
        private set

    // ─── Domain Layer ──────────────────────────────────────────────────────────

    lateinit var actionRunner: ActionRunner
        private set

    override fun onCreate() {
        super.onCreate()

        // Data layer
        val passphrase = "offnetpay_secure_db".toByteArray() // In production, derive from secure source
        database = AppDatabase.create(this, passphrase)
        historyRepo = HistoryRepository(database.transactionDao())
        prefsRepo = PreferencesRepository(dataStore)

        // Platform layer
        overlayController = OverlayControllerImpl(this)
        ussdEngine = UssdEngine(this, overlayController)
        carrierDetector = CarrierDetector(this)
        qrScannerManager = QrScannerManager()

        // Domain layer
        actionRunner = ActionRunner(ussdEngine)
    }
}

/**
 * Extension property for convenient access to [OffNetPayApplication] from any Context.
 */
val Context.offNetPayApp: OffNetPayApplication
    get() = applicationContext as OffNetPayApplication
