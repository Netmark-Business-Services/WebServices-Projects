def Test1():
    manager = Aliases.HealthEdge_Manager
    home_form = manager.HomeForm
    panel = home_form.panelControlDetail
    docked_bar = home_form.BarDockControl.DockedBarControl

    # --- Step 1: Open Member Search ---
    member_widget = panel.homeTab1.WidgetsHost.WidgetContainer.MemberWidgetControl
    member_widget.xtraScrollableControlMembers.TaskRow.panelControlTop.panelControlTaskLinks.SimpleButtonSearch.ClickButton()

    # --- Step 2: Enter Member ID and View Details ---
    search_dialog = manager.SearchDialog
    member_search_box = search_dialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleMemberSearchCriteria.entityPanelSearchInput.autoEditHccIdentifier.panelControlAutoEdit.TextEdit
    member_search_box.SetText("90673572H")
    member_search_box.TextBoxMaskBox.Keys("[Enter]")
    search_dialog.panelControl1.standaloneBarDockControlTasks.DockedBarControl.ClickItem("View")

    # --- Step 3: Navigate to Correspondence Tab ---
    subscription_panel = panel.SubscriptionView.splitContainerControl1
    subscription_panel.SplitGroupPanel.subscriptionSummary.subscriptionTreeList.entityPanelSubscription.treeListSubscription.ClickCell(0, "Name")
    subscription_panel.SplitGroupPanel2.SubscriptionGeneralView.xtraTabControlSubscription.ClickTab("Correspondence")

    # --- Step 4: Initiate Sending Correspondence ---
    docked_bar.ClickItem("Send Correspondence")
    correspondence_dlg = manager.SendCorrespondenceDlg

    # --- Step 5: Select Member in Correspondence Summary ---
    recipient_panel = correspondence_dlg.panelControlSummary.MemberCorrespondenceSummary.headerGroupControlRecipient.entityPanelCorrespondence.subEntityPanelRecipient.memberLookupControlSummary.subEntityPanelMembership.gridLookUpEditMembers
    recipient_panel.Click(162, 9)
    manager.PopupGridLookUpEditForm.GridControl.ClickCellXY(0, "Member ID", 133, 7)

    # --- Step 6: Choose Correspondence Type ---
    correspondence_details = correspondence_dlg.panelBottom.xtraTabControlEdit.xtraTabPageEdit.CorrespondenceEditControl.xtraScrollableControl1.correspondenceDetails.entityPanelCorrespondence
    correspondence_details.headerGroupControlCorrespondence.lookupCorrespondence.Click(209, 6)
    manager.PopupLookUpEditForm.Click(175, 49)

    # --- Step 7: Confirm Member as Recipient Again ---
    subject_recipient_panel = correspondence_details.headerGroupControlCorrespondenceSubject.subEntityPanelCorrespondenceSubject.memberLookupControl.subEntityPanelMembership.gridLookUpEditMembers
    subject_recipient_panel.Click(164, 9)
    manager.PopupGridLookUpEditForm2.GridControl.ClickCellXY(0, "Name", 1, 6)

    # --- Step 8: Send Correspondence ---
    correspondence_dlg.BarDockControl.DockedBarControl.ClickItem("Send")

    # --- Step 9: Select Reason Code ---
    reason_dialog = manager.PromptForReasonCode
    reason_dialog.panelReason.lookUpEditReasonCode.Click(79, 6)
    manager.PopupLookUpEditForm.Click(65, 37)
    reason_dialog.panelControlBottom.simpleButtonOK.ClickButton()

    # --- Step 10: Return to Home ---
    docked_bar.ClickItem("Home")